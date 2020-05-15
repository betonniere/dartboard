package bzh.leroux.dartboard;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import bzh.leroux.yannick.dartboard.R;

public class MainActivity extends    Activity
                          implements BonjourSniffer.Listener {

    private WebView        mWebView;
    private BonjourSniffer mSniffer;

    // ---------------------------------------------------
    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate (Bundle savedInstanceState) {
        super.onCreate (savedInstanceState);
        setContentView (R.layout.activity_main);

        mSniffer = new BonjourSniffer (this,
                                       this);

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

    // ---------------------------------------------------
    @Override
    protected void onResume () {
        super.onResume ();

        mSniffer.start ("_surcouf._tcp");
    }

    // ---------------------------------------------------
    @Override
    protected void onPause () {
        mSniffer.stop ();
        super.onPause ();
    }

    // ---------------------------------------------------
    @Override
    public void onDartboardFound (String hostAddress,
                                  int    port) {
        mWebView.setVisibility (View.VISIBLE);
        mWebView.loadUrl ("http://" + hostAddress + ":" + port);
    }

    // ---------------------------------------------------
    @Override
    public void onDartboardLost () {
    }
}
