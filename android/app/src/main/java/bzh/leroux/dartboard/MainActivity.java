package bzh.leroux.dartboard;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.res.Configuration;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import bzh.leroux.yannick.dartboard.R;

public class MainActivity extends    Activity
                          implements BonjourSniffer.Listener {

    private View           mImageView;
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

        mImageView = findViewById (R.id.imageView);
        mWebView   = findViewById (R.id.webView);

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

        {
            ViewGroup.LayoutParams layoutParams = mImageView.getLayoutParams ();

            if (getResources ().getConfiguration ().orientation == Configuration.ORIENTATION_PORTRAIT) {

                layoutParams.width  = ViewGroup.LayoutParams.WRAP_CONTENT;
                layoutParams.height = ViewGroup.LayoutParams.MATCH_PARENT;
            } else {
                layoutParams.width  = ViewGroup.LayoutParams.MATCH_PARENT;
                layoutParams.height = ViewGroup.LayoutParams.WRAP_CONTENT;
            }

            mImageView.setLayoutParams (layoutParams);
        }

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
