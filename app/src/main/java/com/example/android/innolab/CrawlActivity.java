package com.example.android.innolab;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

public class CrawlActivity extends AppCompatActivity {
    int id;
    String name;
    TextView textView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_crawl);
        Intent intent=getIntent();
        id=intent.getIntExtra("id",0);
        name=intent.getStringExtra("name");
        textView=(TextView)findViewById(R.id.text1);
    }
    public void onCrawl(View view) {
        CrawlWorker crawlWorker=new CrawlWorker(this,this);
        crawlWorker.execute(String.valueOf(id));
        textView.setText("Crawling For "+name);
    }
}
