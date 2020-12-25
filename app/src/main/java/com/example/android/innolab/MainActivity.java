package com.example.android.innolab;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;

public class MainActivity extends AppCompatActivity implements AsyncResponse{
    EditText UsernameEt,PasswordET;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        UsernameEt=(EditText)findViewById(R.id.etUsername);
        PasswordET=(EditText)findViewById(R.id.etPassword);

    }
    public void OnLogin(View view) {
        String username=UsernameEt.getText().toString();
        String password=PasswordET.getText().toString();
        String type="login";
        BackgroundWorker backgroundWorker=new BackgroundWorker(this);
        backgroundWorker.delegate = this;
        backgroundWorker.execute(type,username,password);
    }
    public void processFinish(String output){
        //this you will received result fired from async class of onPostExecute(result) method.
        if(output.equals("Login Success"))
            startActivity(new Intent(this,MainWorker.class));
    }
    public void OpenReg(View view){
        startActivity(new Intent(this,Register.class));
    }
}
