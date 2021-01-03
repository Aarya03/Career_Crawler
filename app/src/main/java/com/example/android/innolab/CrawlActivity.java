package com.example.android.innolab;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

public class CrawlActivity extends AppCompatActivity {
    int id;
    String name;
    TextView textView;
    ListView listView;
    ImageView imageView;
    TextView instiName;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        assert getSupportActionBar() != null;   //null check
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);   //show back button
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_crawl);
        Intent intent=getIntent();
        id=intent.getIntExtra("id",0);
        name=intent.getStringExtra("name");
        textView=(TextView)findViewById(R.id.text1);
        listView=findViewById(R.id.listView1);
        imageView=findViewById(R.id.insti_logo);
        int drawableId = getResources().getIdentifier("x"+id, "drawable", getPackageName());
        if(drawableId!=0)
            imageView.setImageResource(drawableId);
        else
            imageView.setImageResource(R.drawable.err);
        instiName=findViewById(R.id.insti_name);
        instiName.setText(name);
    }
    @Override
    public boolean onSupportNavigateUp() {
        finish();
        return true;
    }
    public void onCrawl(View view) {
        CrawlWorker crawlWorker=new CrawlWorker(this,this);
        crawlWorker.execute(String.valueOf(id));
        textView.setText("Crawling For "+name);
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                String clickdData=(String) parent.getItemAtPosition(position);

                ClipboardManager clipboard = (ClipboardManager)
                        getSystemService(Context.CLIPBOARD_SERVICE);
                ClipData clip = ClipData.newPlainText("label", clickdData);
                clipboard.setPrimaryClip(clip);
                Toast.makeText(CrawlActivity.this,"Copied "+clickdData+" to Clipboard",Toast.LENGTH_SHORT).show();
            }
        });
    }
}
