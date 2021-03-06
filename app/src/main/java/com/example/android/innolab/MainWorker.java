package com.example.android.innolab;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.widget.AdapterView;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.example.android.innolab.utils.PreferenceUtils;

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
        setTitle("Institutes Near Your Location");
        assert getSupportActionBar() != null;   //null check
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);   //show back button
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_worker);
        e1=(EditText)findViewById(R.id.searchFilter);
        e1.addTextChangedListener(this);
        //Populating data from database..
        loadItems();

    }
    @Override
    public boolean onSupportNavigateUp() {
        finish();
        return true;
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
                            type="University";
                        if(drawableId!=0)
                            itemList.add(new Item(name,"Type Of Institution",type,drawableId,id,home_page));
                        else
                            itemList.add(new Item(name,"Type Of Institution",type,R.drawable.err,id,home_page));
                    }
                    adapter =new itemListAdapter(MainWorker.this,R.layout.adapter_view_layout,itemList);
                    mListView.setAdapter(adapter);
                    mListView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                        @Override
                        public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                            Item item= (Item) parent.getItemAtPosition(position);
                            Intent intent=new Intent(getApplicationContext(),CrawlActivity.class);
                            intent.putExtra("id",item.getID());
                            intent.putExtra("name",item.getName());
                            intent.putExtra("home_page",item.getHomePage());
                            startActivity(intent);
                        }
                    });
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
    public void onLogout(View view){
//        PreferenceUtils.saveEmail(null,this);
//        PreferenceUtils.savePassword(null,this);
//        startActivity(new Intent(this,MainActivity.class));
//        finish();
        showPopup();
    }
    // first step helper function
    private void showPopup() {
        AlertDialog.Builder alert = new AlertDialog.Builder(this);
        alert.setMessage("Are you sure?")
                .setPositiveButton("Logout", new DialogInterface.OnClickListener()                 {

                    public void onClick(DialogInterface dialog, int which) {

                        logout(); // Last step. Logout function

                    }
                }).setNegativeButton("Cancel", null);

        AlertDialog alert1 = alert.create();
        alert1.show();
    }

    private void logout() {
        PreferenceUtils.saveEmail(null,this);
        PreferenceUtils.savePassword(null,this);
        startActivity(new Intent(this, MainActivity.class));
        finish();
    }
}
