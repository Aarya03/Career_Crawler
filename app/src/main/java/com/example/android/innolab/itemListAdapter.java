package com.example.android.innolab;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ArrayAdapter;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.Filter;
import android.widget.Filterable;
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

public class itemListAdapter extends BaseAdapter implements Filterable {
    private static final String TAG="ItemListAdapter";
    ArrayList<Item> items;
    CustomFilter filter;
    ArrayList<Item> filterList;
    private Context mContext;
    private int mResource;
    private int lastPosition=-1;

    @Override
    public Filter getFilter() {
        if(filter==null){
            filter=new CustomFilter();
        }
        return filter;
    }

    static class ViewHolder {
        TextView name;
        TextView birthday;
        TextView sex;
        ImageView img;
        Button button;
    }

    public itemListAdapter(Context context, int resource, @NonNull ArrayList<Item> objects) {
        this.items=objects;
        this.filterList=objects;
        mContext=context;
        mResource=resource;
    }

    @Override
    public int getCount() {
        return items.size();
    }

    @Override
    public Object getItem(int position) {
        return items.get(position);
    }

    @Override
    public long getItemId(int position) {
        return items.indexOf(getItem(position));
    }

    @NonNull
    @Override
    public View getView(final int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        //get the items information
        String name=items.get(position).getName();
        String birthday=items.get(position).getBirthday();
        String sex=items.get(position).getSex();
        int imgID=items.get(position).getImgURL();

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
    class CustomFilter extends Filter{

        @Override
        protected FilterResults performFiltering(CharSequence constraint) {
            FilterResults results=new FilterResults();
            if(constraint!=null&&constraint.length()>0){
                constraint=constraint.toString().toUpperCase();
                ArrayList<Item> filters=new ArrayList<>();
                for(int i=0;i<filterList.size();i++){
                    if(filterList.get(i).getName().toUpperCase().contains(constraint)){
                        Item item=new Item(filterList.get(i).getName(),filterList.get(i).getBirthday(),filterList.get(i).getSex(),filterList.get(i).getImgURL(),filterList.get(i).getID(),filterList.get(i).getHomePage());
                        filters.add(item);
                    }
                }
                results.count=filters.size();
                results.values=filters;
            }
            else{
                results.count=filterList.size();
                results.values=filterList;
            }
            return results;
        }

        @Override
        protected void publishResults(CharSequence constraint, FilterResults results) {
            items=(ArrayList<Item>)results.values;
            notifyDataSetChanged();
        }
    }
}
