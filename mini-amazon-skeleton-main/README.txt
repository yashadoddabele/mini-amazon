Team Members
- Isha Shah: Users Guru
- Tanvi Poondota: Products Guru
- Naveen Siva: Sellers Guru
- Yasha Doddabele: Carts Guru

Team Name: Prime Team
GitLab link: https://gitlab.oit.duke.edu/ids10/mini-amazon-skeleton

Final Demo Video Link: 
https://drive.google.com/file/d/16er_4P2Gr7h0LUd1NzSsG_cbJPFUL5Vr/view?usp=drive_link
** There were issues uploading to gradescope due to the number of images in the random_images folder, therefore we decided to delete the folder from the zip file submitted. This folder just included the png files for all 2000 images. 



Milestone 4 Demo Video Link: https://duke.zoom.us/rec/share/S9PoC7pMcfla2L6bDj3MBP6JR1zG1fD3AYZsASiyXWSJkcvD6kQ7jntOWBvBg_dF.n2IgrrrBljxvg2GY?startTime=1699591504000
https://duke.zoom.us/rec/share/S9PoC7pMcfla2L6bDj3MBP6JR1zG1fD3AYZsASiyXWSJkcvD6kQ7jntOWBvBg_dF.n2IgrrrBljxvg2GY?startTime=1699591504000


Milestone 4: Where to find in your GitLab/GitHub repo the code for creating and populating a much larger database
The code for creating randomized data to populate the csv files that are then loaded into our database via load.sql can be found under db/generated in the gen.py file. The code for generating random images for our products can be found under db/static/css in the generate_images.py file. The images used are stored in the random_images folder under app/static/css. 
** There were issues uploading to gradescope due to the number of images in the random_images folder, therefore we decided to delete the folder from the zip file submitted. 

Milestone 3 Demo Video Link: https://duke.zoom.us/rec/share/-mxYSuH5ucEY7NKeidbeVCIY7D3DwTBnh0o1U2EdBsklcChd2lmTbrwsbsQQRlkd.CdWuh8snqcBXmOsl?startTime=1696531949000

Milestone 3 (where to find in your GitLab/GitHub repo the implementation of required items):

Products feature:
Within the app folder, I worked in the kproducts.py, index.py, and __init__.py files. I also worked in the products.py file within the models folder and updated the base.html, index.html, and kproducts.html files within the tempaltes folder. 

Sellers feature:
Within the app folder, I created the sellerInventory.py and the sellerOrders.py blueprints. I also created two html files for sellersInventory.html, and sellersOrders.html. Additionally, I created two models namely sellerInventory.py and sellerOders.py, which help implement the seller inventory and seller order features. 

Carts feature:
Within the app folder, I created a new file in models called cart_items,py, and within templates I created cart.html, and in the whole folder I created carts.py for API endpoints. In the db folder, under data I created two csv files: Carts and ItemInCart. I also modified create.sql, load.sql (in db) and in app, I modified index.html. 

Users feature:
Within the app folder, I edited purchase.py and created purchasehistory.py. In templates, I also created the history.html file and edited the base.html file. Finally, I edited the __init__.py and index.py file.


Contributions since Milestone 1 (Milestone 2 submission):

Yasha: 
    - I cloned our new GitLab repo and made this text file. I also designed the Cart/Order database schemas by making a rough E/R diagram and translating them into relational schemas. Then, I made a user-facing page design of the Cart and Orders pages.
Tanvi:
    - Since the last milestone, we set up our team’s GitLab repo. I cloned the project and ran it using my container. I drew an ER diagram for the product entity and outlined its relationships to other entities. I outlined a design for each page of the website that contains product information. 
Isha:
    - Since the last milestone, I forked the Github repo and cloned the project in my container. I drew an ER diagram as a User guru and outlined the schemas. I also outlined a design for pages that deal with displaying the user information, purchase history and orders, and account information.
Naveen:
    - Since the last milestone, we've all set up our GitLab repository on our own computers. I've cloned the project to my computer, and my task was to create an ER diagram for the Sellers Guru and how it connects to other parts of the system. I've also worked on designing the Sellers Guru page.
