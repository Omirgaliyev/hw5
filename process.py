import instaloader
import os
import time

def get_post_info(username, password, target_username, post_number):
    # Create an Instaloader object
    L = instaloader.Instaloader()

    try:
        # Check if the session file exists
        session_file = f'.instaloader-{target_username}'
        if os.path.exists(session_file):
            L.load_session_from_file(target_username)
        else:
            # If the session file doesn't exist, log in and save the session
            L.context.login(username, password)
            L.save_session_to_file(target_username)

        # Get the profile of the target user
        profile = instaloader.Profile.from_username(L.context, target_username)

        # Get the specified post
        posts = profile.get_posts()
        post_to_get = None
        for _ in range(post_number):
            post_to_get = next(posts, None)

        # Check if the specified post exists
        if post_to_get:
            # Get post details
            post_url = f"https://www.instagram.com/p/{post_to_get.shortcode}/"
            post_time = post_to_get.date_utc.strftime("%Y-%m-%d %H:%M:%S")
            likes_count = post_to_get.likes

            # Create a unique filename for the post
            filename = f'post_{post_number}.txt'

            # Write post information to the file
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(f"Post URL: {post_url}\n")
                file.write(f"Post Time: {post_time}\n")
                file.write(f"Likes Count: {likes_count}\n\n")

                # Get up to 500 comments for the post
                comments = post_to_get.get_comments()
                for j, comment in enumerate(comments):
                    if j < 500:
                        file.write(f"  {comment.owner.username}: {comment.text}\n")

                file.write("\n")

            print(f"Information for post {post_number} has been saved to {filename}")
        else:
            print(f"No post found for post number {post_number}.")

    except instaloader.exceptions.InstaloaderException as e:
        print(f"An error occurred: {e}")

    time.sleep(5)

# Replace these with your Instagram credentials
username = ""
password = ""

# Replace this with the target Instagram username
target_username = "kudaibergenov.dimash"

# Get information for the second post
get_post_info(username, password, target_username, 20)

