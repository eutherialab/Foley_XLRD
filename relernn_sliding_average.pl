## In the script below, replace DATAFILE with the raw bscorrected output from ReLERNN
## As written, the script averages recombination rates in 2Mb blocks with a step of 50kb. 
## Change hard coded numbers below as required


#!/usr/bin/perl -w
use strict;
use warnings;   


my $average_block=2000000;

my $folder='./';
opendir(FOLDER,"$folder");
my @arrayfile = grep(/DATAFILE/,readdir(FOLDER));
close FOLDER;
my $windowsize=50000;
my $step=50000;
my $number_block=$average_block/$windowsize;


foreach my $filename ( @arrayfile ){

######################################
my $max_loc; 
open (F, "$folder/$filename");
while (<F>){
chomp $_;
unless ($_) {next}
if ($_=~/START/) {next}
if ($_=~/\S+\t(\d+)\t(\d+).+/)   {$max_loc=$2};     #scaffold_m19_p_5	34000	68000	122	3.26E-10

}
close F;

######################################

 my $OUT=$filename;    
 $OUT=~s/.recom.txt/\_$windowsize\_$step\_$average_block\_average\.txt/;
 open (OUT, ">>$OUT");
 print OUT "Chr\tWindows_S\tWindows_E\trate\n";
 
######################################
 
 
 my $region_file=$filename;

 
  open (Region, "$region_file") or die print "can not open region_file\n";
   my @star; my @end; my @recom; my $chrosomoe;
   while (<Region>){
   $_=~s/\r\n//;  chomp $_;
   if ($_=~/start/) {next}
   unless ($_) {next}

   my @aa=split(/\t/,$_);#  scaffold_m19_p_5	34000	68000	122	3.26E-10
   push (@star, $aa[1]); push (@end, $aa[2]); push (@recom, $aa[4]);
   $chrosomoe=$aa[0];
	}
   close Region;	
 
 ######################################
   

	 my $count=0;  my $caculator;  my @block;  my @average;
     for( my $i=1; $i<($max_loc-$windowsize); $i+=$step ){

	 	 for my $j (0..(@star-1)){
	     if (($i >= $star[$j]) and ($i <= $end[$j])) {
		 #print OUT "$i\t$recom[$j]\n"; 
		 push (@average,$recom[$j]);}
	     }
	  
	  $caculator++;   push (@block,$i); 
	  
	  if ($caculator == $number_block){
	   

	   my $sum; my $sum_number=0;
	   for (1..(@average-2))  {
	   
	   if (defined ($average[$_])) {$sum+=$average[$_]; $sum_number++;}
	   }
	   for (0..(@block-1)) {
	   if (($block[$_]) and defined($sum)) {print OUT $chrosomoe,"\t",$block[$_],"\t",$block[$_]+$windowsize,"\t",$sum/$sum_number,"\n";}
	   }
	   @average='';
	   @block='';
	   $caculator=0;
	   #exit;
	   }

	   
	 }
	 	   
	   @average=sort {$a <=> $b}@average;
	   my $sum; my $sum_number=0;
	   for (0..(@average-1))  {$sum+=$average[$_]; $sum_number++;}
	   for (0..(@block-1)) {
	   if ($block[$_]) {print OUT $chrosomoe,"\t",$block[$_],"\t",$block[$_]+$windowsize,"\t",$sum/$sum_number,"\n";}	   }
     close OUT;
}
