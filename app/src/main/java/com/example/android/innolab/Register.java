package com.example.android.innolab;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.EditText;

public class Register extends AppCompatActivity {
    EditText name,surname,age,username,password;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        assert getSupportActionBar() != null;   //null check
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);   //show back button
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);
        name=(EditText)findViewById((R.id.etFirstname));
        surname=(EditText)findViewById((R.id.etSurname));
        age=(EditText)findViewById((R.id.etAge));
        username=(EditText)findViewById((R.id.etUsername));
        password=(EditText)findViewById((R.id.etPassword));

    }
    public void OnReg(View view){
        String str_name=name.getText().toString();
        String str_surname=surname.getText().toString();
        String str_age=age.getText().toString();
        String str_username=username.getText().toString();
        String str_password=password.getText().toString();
        String type="register";
        BackgroundWorker backgroundWorker=new BackgroundWorker(this);
        backgroundWorker.execute(type,str_name,str_surname,str_age,str_username,str_password);
    }
    @Override
    public boolean onSupportNavigateUp() {
        finish();
        return true;
    }
}
