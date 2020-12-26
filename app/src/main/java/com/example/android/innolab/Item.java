package com.example.android.innolab;

public class Item {
    private String Name;
    private String Birthday;
    private String Sex;

    public Item(String name, String birthday, String sex) {
        Name = name;
        Birthday = birthday;
        Sex = sex;
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
