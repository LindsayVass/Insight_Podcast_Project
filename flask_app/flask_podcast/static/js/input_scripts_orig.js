// Do typeahead queries

var podcastResults = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  identify: function(obj) { return obj.name; },
  remote: {
    url: '/autocomplete?q=%QUERY',
    wildcard: '%QUERY'
  }
});


var searchVal;
$('#remote .form-control').keyup(function(){ 
  searchVal = $(this).val(); 
  //console.log("searchVal:" + searchVal);
  //console.log("results: %o", podcastResults);
});

$('#remote .form-control').typeahead({
  highlight: true,
  minLength: 3
},
{  
  limit: 10,
  display: 'name',
  source: podcastResults,
  templates: {
    suggestion: function(data){
      return '<p><a href="/output?id=' + data.id + '">' + data.name + '</a></p>';
    }, 
    empty: '<p>No podcasts found.</p>',
    footer: function() {
      return '<p><a href="/check_input?podcast_name='+ searchVal + '">View all results</a></p>'
    }
  }
});


// Make sure drop-down doesn't go below bottom of window
$( document ).ready(function() {
  $('.tt-dropdown-menu').height(function(index, height) {
    $(this).css('height', window.innerHeight - $(this).offset().top - 50);
  });
});


