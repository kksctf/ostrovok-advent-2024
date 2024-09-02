package com.kksctf.ostrovok24

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.material3.*
import androidx.compose.material3.TopAppBarDefaults.topAppBarColors
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import kotlinx.coroutines.launch
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response


class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MyApp()
        }
    }

    @Composable
    fun BlueButton(onClick: () -> Unit, text: String) {
        Button(
            onClick = onClick,
            colors = ButtonDefaults.buttonColors(
                containerColor = Color(0xFF0D41E2), // Background color
                contentColor = Color.White          // Text color
            ),
            modifier = Modifier
                .width(400.dp)
                .height(100.dp)
        ) {
            Text(text)
        }
    }

    @Composable
    fun MyApp() {
        val navController = rememberNavController()

        NavHost(navController = navController, startDestination = "home") {
            composable("home") {
                HomeScreen(onNavigateToDetail = { message ->
                    navController.navigate("detail/$message")
                })
            }
            composable(
                route = "detail/{message}",
                arguments = listOf(navArgument("message") {type = NavType.StringType})
            ) {backStackEntry ->
                val message = backStackEntry.arguments?.getString("message")
                DetailScreen(message = message)
            }
        }
    }

    @OptIn(ExperimentalMaterial3Api::class)
    @Composable
    fun HomeScreen(onNavigateToDetail: (String) -> Unit) {
        val pressedSequence = remember { mutableStateListOf<Int>() }
        val correctSequence = listOf({_{_{RANDOM_SEQ}_}_})  // TODO: per instance unique list of numbers from 1 to 5, i.e. (1, 4, 5, 2, 1, 1, 5)

        val scope = rememberCoroutineScope()
        val snackbarHostState = remember { SnackbarHostState() }

        val retrofit = Retrofit.Builder()
            .baseUrl("{_{_{BACKEND_URL}_}_}") // TODO: backend url
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        val api = retrofit.create(ApiService::class.java)

        fun showSnackbar(message: String) {
            scope.launch {
                snackbarHostState.showSnackbar(message)
            }
        }

        fun checkSequenceAndTriggerApi() {
            var isSequenceMatching = true
            for (i in pressedSequence.indices) {
                if (pressedSequence[i] != correctSequence[i]) {
                    isSequenceMatching = false
                    break
                }
            }

            if (isSequenceMatching) {
                if (pressedSequence.size == correctSequence.size) {
                    fetchMessage(api::callSecret, onMessageReceived = {
                        onNavigateToDetail(it)
                    })
                    pressedSequence.clear() // Reset sequence after successful match
                }
            } else {
                pressedSequence.clear() // Reset if sequence doesn't match
            }
        }

        fun buttonOnClick(apiCall: () -> Call<Message>, buttonID: Int) {
            pressedSequence.add(buttonID)
            checkSequenceAndTriggerApi()
            fetchMessage(apiCall, onMessageReceived = {
                showSnackbar(it)
            })
        }

        Scaffold(
            snackbarHost = {
                SnackbarHost(hostState = snackbarHostState)
            },
            topBar = {
                TopAppBar(
                    colors = topAppBarColors(
                        containerColor = MaterialTheme.colorScheme.surfaceContainer,
                        titleContentColor = MaterialTheme.colorScheme.primary,
                    ),
                    title = {
                        Text(
                            modifier = Modifier
                                .fillMaxWidth(),
                            textAlign = TextAlign.Center,
                            text = "C⭐r⭐a⭐b⭐hotel"
                        )
                    }
                )
            },
            bottomBar = {
                BottomAppBar(
                    containerColor = MaterialTheme.colorScheme.surfaceContainer,
                    contentColor = MaterialTheme.colorScheme.primary,
                ) {
                    Text(
                        modifier = Modifier
                            .fillMaxWidth(),
                        textAlign = TextAlign.Center,
                        text = "made by seagulls",
                    )
                }
            }
        ) { innerPadding ->
            Column(
                modifier = Modifier
                    .padding(innerPadding)
                    .fillMaxWidth(),
                verticalArrangement = Arrangement.spacedBy(16.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
            ) {
                BlueButton({ buttonOnClick(api::callAPI1, 1) }, "Заказ СПА")
                BlueButton({ buttonOnClick(api::callAPI2, 2) }, "Пароль от Wi-Fi")
                BlueButton({ buttonOnClick(api::callAPI3, 3) }, "Уборка номера")
                BlueButton({ buttonOnClick(api::callAPI4, 4) }, "Заказ парковочного места")
                BlueButton({ buttonOnClick(api::callAPI5, 5) }, "Заказ лобстеров")
            }
        }
    }

    @Composable
    fun DetailScreen(message: String?) {
        Column(
            modifier = Modifier.fillMaxSize(),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text("$message")
        }
    }

    private fun fetchMessage(
        apiCall: () -> Call<Message>,
        onMessageReceived: (String) -> Unit
    ) {
        apiCall().enqueue(object : Callback<Message> {
            override fun onResponse(call: Call<Message>, response: Response<Message>) {
                if (response.isSuccessful) {
                    onMessageReceived(response.body()?.message ?: "No message")
                } else {
                    onMessageReceived("Error: ${response.code()}")
                }
            }

            override fun onFailure(call: Call<Message>, t: Throwable) {
                onMessageReceived("Failure: ${t.message}")
            }
        })
    }

    interface ApiService {
        @GET("spa")
        fun callAPI1(): Call<Message>

        @GET("get_wifi")
        fun callAPI2(): Call<Message>

        @GET("cleaning")
        fun callAPI3(): Call<Message>

        @GET("book_parking")
        fun callAPI4(): Call<Message>
        
        @GET("order_lobsters")
        fun callAPI5(): Call<Message>

        @GET("{_{_{RANDOM_STRING_SEQ}_}_}")  // TODO: same url as in python
        fun callSecret(): Call<Message>
    }

    data class Message(val message: String)
}
