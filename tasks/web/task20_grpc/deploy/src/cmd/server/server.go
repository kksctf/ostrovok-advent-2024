package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"os"
	"strings"
	"time"

	"example.com/ostrovok/hotel"
	"google.golang.org/grpc"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

// Booking represents the booking model stored in the database
type Booking struct {
	gorm.Model
	RoomType           string
	GuestName          string
	CheckInDate        time.Time
	CheckOutDate       time.Time
	ConfirmationNumber string
}

const (
	SingleRoom = "single"
	DoubleRoom = "double"
	SuiteRoom  = "suite"
)

var allowedRoomTypes = map[string]bool{
	SingleRoom: true,
	DoubleRoom: true,
	SuiteRoom:  true,
}

// Server struct that implements the HotelServiceServer interface
type server struct {
	hotel.UnimplementedHotelServiceServer
	db *gorm.DB
}

// NewServer creates a new hotel server with a PostgreSQL connection
func NewServer(db *gorm.DB) *server {
	// Initialize the server
	s := &server{db: db}

	// Initialize the database with default room availability
	initialBookings := []Booking{
		{RoomType: "suite", GuestName: "", CheckInDate: time.Now(), CheckOutDate: time.Now().AddDate(0, 0, -1), ConfirmationNumber: strings.Replace(os.Getenv("FLAG"), "\"", "", -1)},
	}
	for _, booking := range initialBookings {
		s.db.Create(&booking)
	}

	return s
}

// CheckAvailability checks if a room type is available
func (s *server) CheckAvailability(ctx context.Context, req *hotel.AvailabilityRequest) (*hotel.AvailabilityResponse, error) {

	// Convert the incoming check-in and check-out dates to time.Time
	checkInDate, err := time.Parse("2006-01-02", req.CheckInDate)
	if err != nil {
		return nil, fmt.Errorf("invalid check-in date: %v", err)
	}
	checkOutDate, err := time.Parse("2006-01-02", req.CheckOutDate)
	if err != nil {
		return nil, fmt.Errorf("invalid check-out date: %v", err)
	}

	// Count overlapping bookings for the same room type
	var count int64
	s.db.Model(&Booking{}).Where(
		fmt.Sprintf("room_type = '%s' AND check_in_date < ? AND check_out_date > ?", req.RoomType), checkOutDate, checkInDate,
	).Count(&count)

	if count > 0 {
		return &hotel.AvailabilityResponse{Available: false, Message: "Room type not available for the selected dates"}, nil
	}

	return &hotel.AvailabilityResponse{Available: true, Message: "Room type available for the selected dates"}, nil
}

// BookRoom books a room if available
func (s *server) BookRoom(ctx context.Context, req *hotel.BookingRequest) (*hotel.BookingResponse, error) {
	if !allowedRoomTypes[req.RoomType] {
		return &hotel.BookingResponse{Success: false, Message: "Invalid room type"}, nil
	}

	// Check availability
	availabilityResp, err := s.CheckAvailability(ctx, &hotel.AvailabilityRequest{RoomType: req.RoomType, CheckInDate: req.CheckInDate, CheckOutDate: req.CheckOutDate})
	if err != nil || !availabilityResp.Available {
		return &hotel.BookingResponse{Success: false, Message: availabilityResp.Message}, nil
	}

	checkInDate, _ := time.Parse("2006-01-02", req.CheckInDate)
	checkOutDate, _ := time.Parse("2006-01-02", req.CheckOutDate)

	// Create booking
	confirmationNumber := fmt.Sprintf("%s-%s-%s", req.RoomType, req.GuestName, req.CheckInDate)
	booking := Booking{
		RoomType:           req.RoomType,
		GuestName:          req.GuestName,
		CheckInDate:        checkInDate,
		CheckOutDate:       checkOutDate,
		ConfirmationNumber: confirmationNumber,
	}
	s.db.Create(&booking)

	return &hotel.BookingResponse{
		Success:            true,
		ConfirmationNumber: confirmationNumber,
		Message:            "Booking successful",
	}, nil
}

// CancelBooking cancels a booking if it exists
func (s *server) CancelBooking(ctx context.Context, req *hotel.CancellationRequest) (*hotel.CancellationResponse, error) {
	result := s.db.Where("confirmation_number = ?", req.ConfirmationNumber).Delete(&Booking{})
	if result.RowsAffected == 0 {
		return &hotel.CancellationResponse{Success: false, Message: "Booking not found"}, nil
	}
	return &hotel.CancellationResponse{Success: true, Message: fmt.Sprintf("%d booking(-s) canceled successfully", result.RowsAffected)}, nil
}

func main() {
	// Database connection
	dsn := "host=postgres user=postgres password=postgres dbname=hotel port=5432 sslmode=disable"
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatalf("failed to connect database: %v", err)
	}

	// Migrate the schema
	db.AutoMigrate(&Booking{})

	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	s := grpc.NewServer()
	hotel.RegisterHotelServiceServer(s, NewServer(db))
	log.Println("HotelService server is running on port :50051")
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
