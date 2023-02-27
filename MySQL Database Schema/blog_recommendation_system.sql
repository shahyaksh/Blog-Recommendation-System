
CREATE TABLE `author` (
  `author_id` int NOT NULL auto_increment,
  `author_name` text NOT NULL,
  `blog_web_name` text NOT NULL,
   primary key (author_id)
);
CREATE TABLE `blogs` (
  `blog_id` int NOT NULL auto_increment,
  `author_id` int NOT NULL,
  `blog_title` text NOT NULL,
  `blog_content` text NOT NULL,
  `blog_link` text NOT NULL,
  `blog_img` text NOT NULL,
  `topic` text NOT NULL,
  `timestamp` datetime NOT NULL,
   primary key (blog_id),
 foreign key (`author_id`) REFERENCES `author` (`author_id`)
);
CREATE TABLE `comment` (
  `comment_id` int NOT NULL auto_increment,
  `user_id` int NOT NULL,
  `blog_id` int NOT NULL,
  `content` text NOT NULL,
  `date_created` int NOT NULL,
  primary key (comment_id),
  FOREIGN KEY (`blog_id`) REFERENCES `blogs` (`blog_id`),
  FOREIGN KEY (`user_id`) REFERENCES `user_profile` (`user_id`)
  
);
CREATE TABLE `favourites` (
  `fav_id` int NOT NULL auto_increment,
  `user_id` int NOT NULL,
  `blog_id` int NOT NULL,
  primary key(`fav_id`),
  FOREIGN KEY (`blog_id`) REFERENCES `blogs` (`blog_id`),
  FOREIGN KEY (`user_id`) REFERENCES `user_profile` (`user_id`)
);
CREATE TABLE `likes` (
  `like_id` int NOT NULL auto_increment,
  `user_id` int NOT NULL,
  `blog_id` int NOT NULL,
  `date_created` datetime NOT NULL,
  primary key (like_id),
 FOREIGN KEY (`blog_id`) REFERENCES `blogs` (`blog_id`),
  FOREIGN KEY (`user_id`) REFERENCES `user_profile` (`user_id`)
);
CREATE TABLE `ratings` (
  `user_id` int NOT NULL,
  `blog_id` int NOT NULL,
  `rating` float NOT NULL,
  `timestamp` datetime NOT NULL,
   FOREIGN KEY (`blog_id`) REFERENCES `blogs` (`blog_id`),
  FOREIGN KEY (`user_id`) REFERENCES `user_profile` (`user_id`)
) ;