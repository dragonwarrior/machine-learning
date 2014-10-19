#!/bin/perl

my $prev_data;
while(<>){
    #2014-10-17,��   23.23   23.30 22.55 23.20 -0.73% 3.21% 6,688,564   153,331,470 2.56 9858
    my $date;
    my $open_price;
    my $max_price;
    my $min_price;
    my $close_price;
    my $inc_rate;

    my $zhen_fu;
    my $zong_shou;
    my $jing_e;
    my $huan_shou;
    my $chengjiao_cishu;
    if (/(\d+)\-(\d+)\-(\d+)\S+\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+([\+\-\.\d]+)/g) {
        $date = $1.$2.$3;
        $open_price = $4;
        $max_price = $5;
        $min_price = $6;
        $close_price = $7;
        $inc_rate = $8;

    } else {
        print "1 invalid data\n".$_;
        next;
    }

    if (/([\+\-\.\d+]+)%\s+(\S+)\s+(\S+)\s+(\S+)\s+(\d+)/g) {
        $zhen_fu = $1;
        $zong_shou = $2;
        $jing_e = $3;
        $huan_shou = $4;
        $chengjiao_cishu = $5;
    } else {
        print "2 invalid data\n".$_;
        next;
    }
    $zong_shou =~ s/,//g;
    $jing_e =~ s/,//g;

    if ($prev_data) {#append inc_rate of the next day
        print $prev_data." ".$inc_rate."\n";
    }
    #backup previouse day

    #$prev_data = $date." ".$open_price." ".$max_price." ".$min_price." ".$close_price." ".$inc_rate;
    $prev_data = $date." ".$open_price." ".$max_price." ".$min_price." ".$close_price." ".$inc_rate;
    $prev_data = $prev_data." ".$zhen_fu." ".$zong_shou." ".$jing_e." ".$huan_shou." ".$chengjiao_cishu;
}
if ($prev_data) {#the last date item
    $inc_rate = 0.0;
    print $prev_data." ".$inc_rate."\n";
}
