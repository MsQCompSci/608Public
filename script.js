//import d3 library here
import * as d3 from "https://cdn.skypack.dev/d3@7";

$(document).ready(function() {
  // A. Text Reversal
  //Create a function to reverse any word that you type in.
  //This can be typed into either an input
  //box or an alert box, and then print the result in a box or on the webpage.
  $("#reverse-text").keyup(function() {
    $("#postReverse").val(
      $("#reverse-text")
        .val()
        .split("")
        .reverse()
        .join("")
    );
  });
/* ----------==============================================================*/
  //Create a function that takes an input number, and prints a table with the 
  //first 20 multiples ofthe number, in order 5x4
  
  // B. Create multiple tables
  var multiplier = 1;
  for (var row = 1; row <= 5; row++) {
    $("#numbersTable").append("<tr>");
    for (var col = 1; col <= 5; col++) {
      $("#numbersTable").append(
        '<td id="' + multiplier++ + '" class="numberHolder"></td>'
      );
    }
    $("#numbersTable").append("</tr>");
  }

  // Multiples
  $("#numbers-for-multiples").keyup(function() {
    //var numbersForMultiples = $("#numbers-for-multiples").val();
    $(".numberHolder").each(function() {
      $(this).html($("#numbers-for-multiples").val() * $(this).attr("id"));
    });
  });

  //C. Presidents Name search
  //Write a function to load the presidents.csv data and display the data as 
  //an html table (you may use a cdv parser from any available library, though 
  //I encourage you to try the d3 one). - Coulndt do with d3 in time
  $('#load_data').click(function(){
  $.ajax({
   url:"https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module5/data/presidents.csv",
   dataType:"text",
   success:function(data)
   {
    var presidents_data = data.split(/\r?\n|\r/);
    var table_data = '<table class="table table-bordered table-striped">';
    for(var count = 0; count<presidents_data.length; count++)
    {
     var cell_data = presidents_data[count].split(",");
     table_data += '<tr>';
     for(var cell_count=0; cell_count<cell_data.length; cell_count++)
     {
      if(count === 0)
      {
       table_data += '<th>'+cell_data[cell_count]+'</th>';
      }
      else
      {
       table_data += '<td>'+cell_data[cell_count]+'</td>';
      }
     }
     table_data += '</tr>';
    }
    table_data += '</table>';
    $('#presidents_table').html(table_data);
   }
  });
 });
  
  
  
  
  
})