$(document).ready(function() {
	window.fbAsyncInit = function() {
		FB.init({appId: '205425319498174',
			status: true,
			cookie: true,
			xfbml: true});

		FB.api('/me', function(response) {
			me = response
		});
                FB.login();

	    refresh_pair = function() {
			$('#left').hide();
			$('#right').hide();
			$('.question').hide();
			$('#friend1').attr('src', '/static/images/avatar.jpg');
			$('#friend2').attr('src', '/static/images/avatar.jpg');
			$('.progress').show();

	        FB.api('/me/friends', function(response) {
	          friends = response['data']

	          rand_friend = function() {
	            return friends[Math.floor(Math.random()*friends.length)];
	          }

	          f1 = rand_friend();
	          f2 = rand_friend();
			$('.name1').text(f1.name);
			$('.name2').text(f2.name);
	          profile_pic = function(id) { return 'http://graph.facebook.com/' + id + '/picture?type=large'; }
				$('#friend1').attr('src', profile_pic(f1.id));
				$('#friend2').attr('src', profile_pic(f2.id));
				$('#left').fadeIn('slow');
				$('#right').fadeIn('slow');
				$('.question').fadeIn('slow');
				$('.progress').fadeOut('fast');
				$('.title').textfill({ maxFontPixels: 34,innerTag: 'h2' });
				$('.name').textfill({ maxFontPixels: 28});
	        });
	    }
	    refresh_pair();

	    setCompatibility = function(rating) {
	        params = "?rating=" + rating;
	        params += "&f1_id=" + f1.id;
	        params += "&f1_name=" + f1.name;
	        params += "&f2_id=" + f2.id;
	        params += "&f2_name=" + f2.name;
	        params += "&rater=" + me.id;
	        params += "&rater_name=" + me.name;
	        $.ajax({
	          url: "/ajax/set_compatibility" + params,
	          success: function(data, status){
					if(data != "okay") { alert(data); }
	          }
	        });
			
	        refresh_pair();
	    }
	
		// matches page
		
		profile_pic = function(id) { return 'http://graph.facebook.com/' + id + '/picture?type=normal'; }

	    get_name = function(id) { 
	        FB.api('/' + id, function(response) {
	          response
	        });
	    }
	    FB.login();

	    get_matches = function(me_id) {
	        params = '?fid=' + me_id
	        $.ajax({
	          url: "ajax/matches" + params,
	          success: function(data, status){
				$('.progress').fadeOut('fast');
	            for(i in data) {
					rating = Math.round(data[i].rating/5*100)
					if (rating >= 90) 
						compatibility = 'super'
					else if (rating >= 80)
						compatibility = 'good'
					else if (rating >= 70)
						compatibility = 'average'
					else if (rating >= 60)
						compatibility = 'poor'
	                html = '<div class="profile">'
					html += '<img src="' + profile_pic(data[i].match_id) + '"> </img>'
					html += '<div class="result ' + compatibility + '"><span>' + rating + '</span><br />out of 100</div>'
	                html += '<p>Your compatibility with <strong>' + data[i].match_name + '</strong> is <strong class="upper">' + compatibility + '</strong><br />'
	                html += '<span>according to ' + data[i].raters + '</span></p>'
	                html += '<div class="clear"></div></div>'
	                $('#matches').append(html)
	            }
	          }
	        });
	    }

	    FB.api('/me', function(response) {
	      me = response
	      HACK = 630308744
	      //HACK = me.id
	      get_matches(HACK)
	    });

	  };
	  (function() {
	    var e = document.createElement('script'); e.async = true;
	    e.src = document.location.protocol +
	      '//connect.facebook.net/en_US/all.js';
	    document.getElementById('fb-root').appendChild(e);
	  }());
	
	$('#star').ratings(5).bind('ratingchanged', function(event, data) {
		setCompatibility(data.rating);
		containerElement.rating = 0;
	});
	$('.name').textfill();
});
