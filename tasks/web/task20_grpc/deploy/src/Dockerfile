# Use an official Golang image as a parent image
FROM golang:latest

# Set the Current Working Directory inside the container
WORKDIR /app

# Copy the Go Modules manifests
COPY go.mod go.sum ./

# Install dependencies
RUN go mod download

# Copy the source from the current directory to the Working Directory inside the container
COPY . .

# Build the Go app
RUN go build -o /hotelservice cmd/server/server.go

# Expose port 50051 to the outside world
EXPOSE 50051

# Command to run the executable
CMD ["/hotelservice"]