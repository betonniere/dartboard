package bzh.leroux.dartboard;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import bzh.leroux.yannick.dartboard.R;

public class MainActivity extends Activity {

    private WebView mWebView;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate (Bundle savedInstanceState) {
        super.onCreate (savedInstanceState);
        setContentView (R.layout.activity_main);

        mWebView = findViewById (R.id.webView);

        {
            final WebSettings settings = mWebView.getSettings ();

            settings.setJavaScriptEnabled                (true);
            settings.setMediaPlaybackRequiresUserGesture (false);
        }

        mWebView.setWebViewClient(new WebViewClient () {
            @Override
            public boolean shouldOverrideUrlLoading (WebView view,
                                                     String  url) {
                return false;
            }

        });
    }

    @Override
    protected void onResume () {
        super.onResume ();

        mWebView.loadUrl ("http://192.168.0.34:8080");
    }
}
