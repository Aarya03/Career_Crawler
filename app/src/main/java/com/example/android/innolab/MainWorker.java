package com.example.android.innolab;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.ListView;

import java.util.ArrayList;

public class MainWorker extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_worker);
        ListView mListView=(ListView)findViewById(R.id.list_view);
        Item john = new Item("John","12-20-1998","Male");
        Item steve = new Item("Steve","08-03-1987","Male");
        Item stacy = new Item("Stacy","11-15-2000","Female");
        Item ashley = new Item("Ashley","07-02-1999","Female");
        Item matt = new Item("Matt","03-29-2001","Male");
        Item matt2 = new Item("Matt2","03-29-2001","Male");
        Item matt3 = new Item("Matt3","03-29-2001","Male");
        Item matt4 = new Item("Matt4","03-29-2001","Male");
        Item matt5 = new Item("Matt5","03-29-2001","Male");
        Item matt6 = new Item("Matt6","03-29-2001","Male");
        Item matt7 = new Item("Matt7","03-29-2001","Male");
        Item matt8 = new Item("Matt8","03-29-2001","Male");
        Item matt9 = new Item("Matt9","03-29-2001","Male");
        Item matt10 = new Item("Matt10","03-29-2001","Male");
        Item matt11 = new Item("Matt11","03-29-2001","Male");

        ArrayList<Item> itemList = new ArrayList<>();
        itemList.add(john);
        itemList.add(steve);
        itemList.add(stacy);
        itemList.add(ashley);
        itemList.add(matt);
        itemList.add(matt2);
        itemList.add(matt3);
        itemList.add(matt4);
        itemList.add(matt5);
        itemList.add(matt6);
        itemList.add(matt7);
        itemList.add(matt8);
        itemList.add(matt9);
        itemList.add(matt10);
        itemList.add(matt11);

        itemListAdapter adapter =new itemListAdapter(this,R.layout.adapter_view_layout,itemList);
        mListView.setAdapter(adapter);
    }
}
