package com.example.android.innolab;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import java.util.ArrayList;
import java.util.List;

public class itemListAdapter extends ArrayAdapter<Item> {
    private static final String TAG="ItemListAdapter";
    private Context mContext;
    private int mResource;
    private int lastPosition=-1;
    static class ViewHolder {
        TextView name;
        TextView birthday;
        TextView sex;
    }

    public itemListAdapter(Context context, int resource, @NonNull ArrayList<Item> objects) {
        super(context, resource, objects);
        mContext=context;
        mResource=resource;
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        //get the items information
        String name=getItem(position).getName();
        String birthday=getItem(position).getBirthday();
        String sex=getItem(position).getSex();

        //create the item objects with information
        Item item=new Item(name,birthday,sex);

        final View result;
        ViewHolder holder;

        if(convertView==null){
            LayoutInflater inflater=LayoutInflater.from(mContext);
            convertView = inflater.inflate(mResource,parent,false);
            holder = new ViewHolder();
            holder.name = (TextView) convertView.findViewById(R.id.textView1);
            holder.birthday = (TextView) convertView.findViewById(R.id.textView2);
            holder.sex = (TextView) convertView.findViewById(R.id.textView3);
            result=convertView;
            convertView.setTag(holder);
        }
        else{
            holder=(ViewHolder)convertView.getTag();
            result=convertView;
        }


        Animation animation= AnimationUtils.loadAnimation(mContext,(position>lastPosition)? R.anim.load_down_anim : R.anim.load_up_anim);
        result.startAnimation(animation);
        lastPosition=position;

        holder.name.setText(name);
        holder.birthday.setText(birthday);
        holder.sex.setText(sex);
        return convertView;

    }
}
