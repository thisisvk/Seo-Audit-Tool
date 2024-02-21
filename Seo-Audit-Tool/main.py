from fpdf import FPDF
import time
from bs4 import BeautifulSoup
import requests
import re
import sys

# Check if a URL argument is provided
if len(sys.argv) < 2:
    print("Usage: python main.py <web_url>")
    sys.exit(1)

url = sys.argv[1]  # Get the URL from command-line arguments

f = open('index.txt', 'w')

response = requests.get(url)
html_text = response.text
soup = BeautifulSoup(html_text, 'lxml')
pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 18)

#----------------------------------------------------------------------------------------
pdf.write(10, '\n')
pdf.write(10, "Is WebPage has a Doctype declaration or not" + "\n")
pdf.write(10, "-------------------------------------------------" + "\n")

#----------------------------------------------------------------------------------------
# Check if the first line of HTML code contains a DOCTYPE declaration
doctype_declared = response.text.strip().startswith('<!DOCTYPE')
if doctype_declared:
    pdf.write(10, f'The website {url} has a DOCTYPE declaration.' + "\n")
else:
    pdf.write(10, f'The website {url} does not have a DOCTYPE declaration.' + "\n")
#----------------------------------------------------------------------------------------
pdf.write(10, '\n')
pdf.write(10, "Total No. of Img Tags and Empty alt attribute" + "\n")
pdf.write(10, "-------------------------------------------------" + "\n")

#----------------------------------------------------------------------------------------
# Check Img tags and alt attribute
total_no_of_img_tag = soup.find_all('img')
pdf.write(10, "Total no of img tag: " + str(len(total_no_of_img_tag)) + "\n")
# Count the number of empty alt attributes
empty_alt_count = 0
for img in total_no_of_img_tag:
    if img.get('alt') == '':
        empty_alt_count += 1
pdf.write(10, 'No of empty Alt attribute in img: ' + str(empty_alt_count) + "\n")
#----------------------------------------------------------------------------------------
pdf.write(10, '\n')
pdf.write(10, "Page Title" + "\n")
pdf.write(10, "-------------------------------------------------" + "\n")

#----------------------------------------------------------------------------------------
# Check title
title = soup.find('title').text
pdf.write(10, 'Your Page Title:' + str(title) + "\n")
#----------------------------------------------------------------------------------------
pdf.write(10, '\n')
pdf.write(10, "Page Headings tag H1,H2 and H3" + "\n")
pdf.write(10, "-------------------------------------------------" + "\n")

#----------------------------------------------------------------------------------------
# Check Headings tag H1,H2 and H3
h1 = soup.find_all('h1')
pdf.write(10, 'Total no of h1 tags:' + str(len(h1)) + "\n")
for h1 in h1:
    pdf.write(10, h1.text)
    pdf.write(10, '\n')
h2 = soup.find_all('h2')
pdf.write(10, 'Total no of h2 tags:' + str(len(h2)) + "\n")
for h2 in h2:
    pdf.write(10, h2.text)
    pdf.write(10, '\n')
h3 = soup.find_all('h3')
pdf.write(10, 'Total no of h3 tags:' + str(len(h3)) + "\n")
for h3 in h3:
    pdf.write(10, h3.text)
    pdf.write(10, '\n')
# h4 = soup.find_all('h4')
# pdf.write(10,'Total no of h4 tags:',len(h4))
# for h4 in h4:
#     pdf.write(10,h4.text)
# h5 = soup.find_all('h5')
# pdf.write(10,'Total no of h5 tags:',len(h5))
# for h5 in h5:
#     pdf.write(10,h5.text)
# h6 = soup.find_all('h6')
# pdf.write(10,'Total no of h6 tags:',len(h6))
# for h6 in h6:
#     pdf.write(10,h6.text)
#----------------------------------------------------------------------------------------
pdf.write(10, '\n')
pdf.write(10, "Minified Js or Not" + "\n")
pdf.write(10, "-------------------------------------------------" + "\n")

#----------------------------------------------------------------------------------------
# Search for common patterns in minified JavaScript files
minified_pattern_1 = r'\bfunction *\('
minified_pattern_2 = r'\{ *[\r\n]+ *\w+:'
minified_pattern_3 = r';\w+\.\w+\.\w+\(\)'

if re.search(minified_pattern_1, response.text) and \
   re.search(minified_pattern_2, response.text) and \
   re.search(minified_pattern_3, response.text):
    pdf.write(10, f'The JavaScript file at {url} is likely minified.' + "\n")
else:
    pdf.write(10, f'The JavaScript file at {url} is not minified.' + "\n")
#----------------------------------------------------------------------------------------
pdf.write(10, '\n')
pdf.write(10, "The meta description tag" + "\n")
pdf.write(10, "-------------------------------------------------" + "\n")

#----------------------------------------------------------------------------------------
# Find the meta description tag
meta_description = soup.find('meta', attrs={'name': 'description'})

# Check the length of the content attribute of the meta description tag
if meta_description and len(meta_description['content']) > 0:
    meta_desc_length = len(meta_description['content'])
    pdf.write(10, f'The website {url} has a meta description with length {meta_desc_length}.' + "\n")
else:
    pdf.write(10, f'The website {url} does not have a meta description.' + "\n")
#----------------------------------------------------------------------------------------
pdf.write(10, '\n')
pdf.write(10, "All HTML tags that have a Inline Css" + "\n")
pdf.write(10, "-------------------------------------------------" + "\n")

#----------------------------------------------------------------------------------------
# Find all HTML tags that have a style attribute set
inline_css_tags = soup.find_all(lambda tag: tag.has_attr('style'))

if inline_css_tags:
    pdf.write(10, f"The website {url} has {len(inline_css_tags)} tags with inline CSS styles:" + "\n")
    # for tag in inline_css_tags:
    #     pdf.write(10,f"- {tag.name}: {tag['style']}")
else:
    pdf.write(10, f"The website {url} does not have any tags with inline CSS styles." + "\n")
#----------------------------------------------------------------------------------------
pdf.write(10, '\n')
pdf.write(10, "Cache techinque" + "\n")
pdf.write(10, "-------------------------------------------------" + "\n")

#----------------------------------------------------------------------------------------
# Cache techinque
if 'Cache-Control' in response.headers:
    pdf.write(10, f"The website {url} is using caching." + "\n")
else:
    pdf.write(10, f"The website {url} is not using caching." + "\n")
#----------------------------------------------------------------------------------------
pdf.write(10, '\n')
pdf.write(10, "Check Robots.txt file is accessible or not" + "\n")
pdf.write(10, "-------------------------------------------------" + "\n")

#----------------------------------------------------------------------------------------
# Define the website you want to check
website_url = url

# Send an HTTP GET request to the website's robots.txt file
robots_txt_url = f"{website_url}/robots.txt"
response = requests.get(robots_txt_url)

# Check if the robots.txt file exists and can be accessed
if response.status_code == 200:
    pdf.write(10, f"The robots.txt file of {website_url} is accessible." + "\n")
    # pdf.write(10,"Contents of the robots.txt file:")
    # pdf.write(10,response.text)
else:
    pdf.write(10, f"The robots.txt file of {website_url} is not accessible." + "\n")
#----------------------------------------------------------------------------------------
pdf.write(10, '\n')
pdf.write(10, "Response Time of WebPage" + "\n")
pdf.write(10, "-------------------------------------------------" + "\n")

#----------------------------------------------------------------------------------------
# Send an HTTP GET request to the website and record the time it takes to receive a response
start_time = time.time()
response = requests.get(url)
end_time = time.time()

# Calculate the response time in seconds
response_time = end_time - start_time

pdf.write(10, f"The website {url} took {response_time:.2f} seconds to respond.")
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
pdf.output('output.pdf')

