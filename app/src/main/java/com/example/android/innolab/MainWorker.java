package com.example.android.innolab;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

public class MainWorker extends AppCompatActivity implements TextWatcher {
    private static final String Item_URL="http://192.168.43.9/AndroidMysqlPHP/Main.php";
    EditText e1;
    itemListAdapter adapter;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_worker);
        e1=(EditText)findViewById(R.id.searchFilter);
        e1.addTextChangedListener(this);
        //Populating data from database..
        loadItems();

    }
    private void loadItems(){
        final ListView mListView=(ListView)findViewById(R.id.list_view);
        final ArrayList<Item> itemList = new ArrayList<>();
        StringRequest stringRequest=new StringRequest(Request.Method.GET, Item_URL, new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                try {
                    JSONArray items=new JSONArray(response);
                    for(int i=0;i<items.length();i++){
                        JSONObject itemObject=items.getJSONObject(i);
                        int id=itemObject.getInt("id");
                        String name=itemObject.getString("name");
                        String home_page=itemObject.getString("home_page");
                        String type=itemObject.getString("type");
                        int drawableId = getResources().getIdentifier("x"+id, "drawable", getPackageName());
                        if(type.equals("null"))
                            type="Not Fetched";
                        itemList.add(new Item(name,"Type Of Institution",type,drawableId,id));
                    }
                    adapter =new itemListAdapter(MainWorker.this,R.layout.adapter_view_layout,itemList);
                    mListView.setAdapter(adapter);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Toast.makeText(MainWorker.this,error.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
        Volley.newRequestQueue(this).add(stringRequest);
    }

    @Override
    public void beforeTextChanged(CharSequence s, int start, int count, int after) {

    }

    @Override
    public void onTextChanged(CharSequence s, int start, int before, int count) {
        this.adapter.getFilter().filter(s);
    }

    @Override
    public void afterTextChanged(Editable s) {

    }
}
