package com.example.android.innolab;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.nostra13.universalimageloader.cache.memory.impl.WeakMemoryCache;
import com.nostra13.universalimageloader.core.DisplayImageOptions;
import com.nostra13.universalimageloader.core.ImageLoader;
import com.nostra13.universalimageloader.core.ImageLoaderConfiguration;
import com.nostra13.universalimageloader.core.assist.ImageScaleType;
import com.nostra13.universalimageloader.core.display.FadeInBitmapDisplayer;

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
        ImageView img;
        Button button;
    }

    public itemListAdapter(Context context, int resource, @NonNull ArrayList<Item> objects) {
        super(context, resource, objects);
        mContext=context;
        mResource=resource;
    }

    @NonNull
    @Override
    public View getView(final int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        //get the items information
        String name=getItem(position).getName();
        String birthday=getItem(position).getBirthday();
        String sex=getItem(position).getSex();
        int imgID=getItem(position).getImgURL();

        final View result;
        ViewHolder holder;

        if(convertView==null){
            LayoutInflater inflater=LayoutInflater.from(mContext);
            convertView = inflater.inflate(mResource,parent,false);
            holder = new ViewHolder();
            holder.name = (TextView) convertView.findViewById(R.id.textView1);
            holder.birthday = (TextView) convertView.findViewById(R.id.textView2);
            holder.sex = (TextView) convertView.findViewById(R.id.textView3);
            holder.img=(ImageView)convertView.findViewById(R.id.image);
            holder.button=(Button)convertView.findViewById(R.id.crawl);
            holder.button.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Toast.makeText(getContext(),"Button was clicked for list item "+position,Toast.LENGTH_SHORT).show();
                }
            });
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
        holder.img.setImageResource(imgID);

        return convertView;

    }
}
