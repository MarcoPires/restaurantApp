data = {
	'upload_folder' : '/var/www/html/restaurantApp/restaurantApp/static/img/uploads',
	'read_folder' : 'static/img/uploads',
	'allowed_extensions' : ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'],
	
	'google_data' : '/var/www/html/restaurantApp/restaurantApp/data/gg_client_secrets.json',
	'google_access_token_check' : 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=',
	'google_user_info' : 'https://www.googleapis.com/oauth2/v1/userinfo',
	'google_logout' : 'https://accounts.google.com/o/oauth2/revoke?token=%s',

	'facebook_data' : '/var/www/html/restaurantApp/restaurantApp/data/fb_client_secrets.json',
	'facebook_access_token_check' : 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s',
	'facebook_me_endpoint' : 'https://graph.facebook.com/v2.4/me',
	'facebook_logout' : 'https://graph.facebook.com/%s/permissions?access_token=%s'
}
