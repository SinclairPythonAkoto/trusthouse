# Trust House 0.2 #

A basic Flask app that allows users to write a review for a property, or search for a property listing and their review before moving in.

Users can upload a rating of a property and include pictures if they so choose.

Reviews will be uploaded anonymously - they just need to select *tenant, neighbour or vistor*.


### API Queries ###
Users can query the *Trust House* databse within the web browser, the data returned will be in a **JSON** file.

#### Get All Addresses ####
- `/API/address`

#### Get All Rviews ####
- `/API/reviews`

#### Filter Reviews By Rating ####
- `/API/rating/...`

#### Filter Reviews By Door Number ####
- `/API/door/...`

#### Filter Reviews By Street Name ####
- `/API/street/`

#### Filter Reviews By Town ####
- `/API/town/...`

#### Filter Reviews By City ####
- `/API/city/...`

#### Filter Reviews By Postcode ####
- `/API/postcode/...`
