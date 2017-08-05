# Instructions

## Pre-Requisites
* Python
* Python bindings for Selenium
* Chrome WebDriver

### Downloading Python bindings for Selenium
`pip install selenium`
 
### Downloading Browser Drivers
Selenium requires a driver to interface with the chosen browser.
Get the required drivers from here

Browser | Driver Link
------- | -----------
Chrome | https://sites.google.com/a/chromium.org/chromedriver/downloads
Edge | https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
Firefox | https://github.com/mozilla/geckodriver/releases
Safari | https://webkit.org/blog/6900/webdriver-support-in-safari-10/

Once the driver files are downlaoded, copy them to /usr/bin or /usr/local/bin

## Database tables
* Create a schema. Change the name of the shcema in the code to the name of your schema.
* Create a table using this script:
```
CREATE TABLE `real_estate_listings` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `created_ts` datetime NOT NULL,
  `source_id` int(10) unsigned NOT NULL,
  `posted_time` datetime NOT NULL,
  `title` varchar(200) CHARACTER SET utf8mb4 NOT NULL DEFAULT '',
  `link` varchar(500) NOT NULL DEFAULT '',
  `source_listing_id` varchar(20) NOT NULL DEFAULT '',
  `location` varchar(200) CHARACTER SET utf8mb4 NOT NULL DEFAULT '',
  `category` varchar(100) CHARACTER SET utf8mb4 NOT NULL DEFAULT '',
  `message` text NOT NULL,
  `contact_name` varchar(100) NOT NULL DEFAULT '',
  `contact_phone_numbers` varchar(100) NOT NULL DEFAULT '',
  `contact_email_addresses` varchar(300) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1015 DEFAULT CHARSET=latin1;
```
