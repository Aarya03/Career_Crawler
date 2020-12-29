package com.example.android.innolab;

public class Item {
    private String Name;
    private String Birthday;
    private String Sex;
    private int imgURL;
    private int ID;

    public Item(String name, String birthday, String sex, int IMGURL,int id) {
        Name = name;
        Birthday = birthday;
        Sex = sex;
        imgURL=IMGURL;
        ID=id;
    }

    public int getID() {
        return ID;
    }

    public void setID(int ID) {
        this.ID = ID;
    }

    public int getImgURL() {
        return imgURL;
    }

    public void setImgURL(int imgURL) {
        this.imgURL = imgURL;
    }

    public String getName() {
        return Name;
    }

    public void setName(String name) {
        this.Name = name;
    }

    public String getBirthday() {
        return Birthday;
    }

    public void setBirthday(String birthday) {
        this.Birthday = birthday;
    }

    public String getSex() {
        return Sex;
    }

    public void setSex(String sex) {
        this.Sex = sex;
    }
}
