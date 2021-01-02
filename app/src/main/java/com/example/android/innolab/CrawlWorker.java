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
import android.widget.ArrayAdapter;
import android.widget.ListView;
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
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

public class CrawlWorker extends AsyncTask<String,Void,String> {
    private Context context;
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
    }

    @Override
    protected void onPostExecute(String result) {
        Activity activity = (Activity) mWeakActivity.get();
        final TextView textView;
        textView=activity.findViewById(R.id.text1);
        textView.setMovementMethod(new ScrollingMovementMethod());
        String fresult=getRes(result);
        String[] lines = fresult.split("\\r?\\n");
        Set<String> hash_Set
                = new HashSet<String>();
        for(int i=0;i<lines.length;i++){
            hash_Set.add(lines[i]);
        }
        String[] ret=new String[hash_Set.size()];
        Iterator<String> it = hash_Set.iterator();
        int idx=0;
        while(it.hasNext()){
            ret[idx++]=it.next();
        }
        ArrayAdapter<String> itemsAdapter =
                new ArrayAdapter<String>(context, android.R.layout.simple_list_item_1,ret);
        ListView listView1=activity.findViewById(R.id.listView1);
        listView1.setAdapter(itemsAdapter);
        textView.setText("Crawled");
    }
    private String getRes(String in){
        in="#"+in;
        String out="";
        for(int i=0;i<in.length()-1;i++){
            if(in.charAt(i)=='<')
                break;
            if(in.charAt(i)=='#'){
                if(i==0)
                    out=out;
                else
                    out=out+'\n';
            }
            else
                out=out+in.charAt(i);
        }
        return out;
    }
    @Override
    protected void onProgressUpdate(Void... values) {
        super.onProgressUpdate(values);
    }
}
