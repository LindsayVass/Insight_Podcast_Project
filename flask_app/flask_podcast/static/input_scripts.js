var podcastResults = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  remote: {
    url: '{{url_for('autocomplete')}}?q=%QUERY',
    wildcard: '%QUERY'
  }
});

var searchVal;
$('#remote .form-control').keyup(function(){ searchVal = $(this).val();} );

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
      return '<p><a href="{{url_for('podcast_output')}}?id=' + data.id + '">' + data.name + '</a></p>';
    }, 
    empty: '<p>No podcasts found.</p>',
    footer: function() {
      return '<p><a href="{{url_for('podcast_check_input')}}?podcast_name='+ searchVal + '">View all results</a></p>'
    }
  }
});