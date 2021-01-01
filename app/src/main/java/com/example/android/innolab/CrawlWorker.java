package com.example.android.innolab;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.text.ClipboardManager;
import android.text.method.ScrollingMovementMethod;
import android.util.Log;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.lang.ref.WeakReference;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLEncoder;

public class CrawlWorker extends AsyncTask<String,Void,String> {
    private Context context;
    private AlertDialog alertDialog;
    private WeakReference mWeakActivity;
    CrawlWorker(Context ctx, Activity activity){
        context =ctx;
        mWeakActivity = new WeakReference<Activity>(activity);
    }

    @Override
    protected String doInBackground(String... params) {
        String sURL="http://192.168.43.9/AndroidMysqlPHP/crawl.php";
        try {
            String id=params[0];
            URL url = new URL(sURL);
            HttpURLConnection httpURLConnection = (HttpURLConnection)url.openConnection();
            httpURLConnection.setRequestMethod("POST");
            httpURLConnection.setDoOutput(true);
            httpURLConnection.setDoInput(true);
            OutputStream outputStream = httpURLConnection.getOutputStream();
            BufferedWriter bufferedWriter = new BufferedWriter(new OutputStreamWriter(outputStream, "UTF-8"));
            String post_data = URLEncoder.encode("id","UTF-8")+"="+URLEncoder.encode(id,"UTF-8");
            bufferedWriter.write(post_data);
            bufferedWriter.flush();
            bufferedWriter.close();
            outputStream.close();
            InputStream inputStream = httpURLConnection.getInputStream();
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream,"iso-8859-1"));
            String result="";
            String line="";
            while((line = bufferedReader.readLine())!= null) {
                result += line;
            }
            bufferedReader.close();
            inputStream.close();
            httpURLConnection.disconnect();
            return result;
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    @Override
    protected void onPreExecute() {
        alertDialog=new AlertDialog.Builder(context).create();

    }

    @Override
    protected void onPostExecute(String result) {
        Activity activity = (Activity) mWeakActivity.get();
        final TextView textView;
        textView=activity.findViewById(R.id.text1);
        textView.setMovementMethod(new ScrollingMovementMethod());
        String fresult=getRes(result);
        textView.setText(fresult);
        textView.setOnClickListener(new View.OnClickListener() { // set onclick listener to my textview
            @Override
            public void onClick(View view) {
                ClipboardManager cm = (ClipboardManager)context.getSystemService(Context.CLIPBOARD_SERVICE);
                cm.setText(textView.getText().toString());
                Toast.makeText(context, "Copied :)", Toast.LENGTH_SHORT).show();
            }
        });
        alertDialog.setTitle("Crawl Status");
        alertDialog.setMessage(result);
//        alertDialog.show();
    }
    private String getRes(String in){
        in=" "+in;
        String out="";
        int c=1;
        for(int i=0;i<in.length()-1;i++){
            if(in.charAt(i)==' ') {
                if(c>1){
                    out+='\n';
                    i+=3;
                }
                out=out+String.valueOf(c++)+". ";
                if(c>2&&c%2==0)
                    out=out+"htt";
            }
            else{
                out=out+in.charAt(i);
            }
        }
        return out;
    }
    @Override
    protected void onProgressUpdate(Void... values) {
        super.onProgressUpdate(values);
    }
}
