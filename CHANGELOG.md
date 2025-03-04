# Change Log

## [1.0.7] 2022-12-09
### Updates and Improvements
- update Bootstrap to v5.2.3
  
## [1.0.6] 2022-06-03
### Updates and Improvements
- update Bootstrap to v5.2.0-beta1
- fix input-group focus issue

## [1.0.5] 2022-03-25
### Update
- update SCSS folder

## [1.0.4] 2022-03-18
### Updates & Bugfixing
- upgrade Bootstrap version to v5.1.3
- upgrade ChartJs plugin version to v3.7.1
- fix running 'npm install' issue
- fix SCSS compiling issues
- update sidebar height
- fix sidebar button on Safari
- update dropdown text on RTL page
- fix navbar scroll error on example pages

## [1.0.3] 2021-06-25
### Updates & Improvements
- upgrade Bootstrap version to v5.0.2
- add new page - Virtual Reality
- add perfectScrollbar for Windows users
- change headings color from '#252F40' to '#344767'
- reduce the 'img' folder size - compress images
- bug fixing
- fix W3 errors

## [1.0.2] 2021-05-10
### Updates & Bugfixing
- upgrade Bootstrap version to v5.0.1
- bug fixing

## [1.0.1] 2021-04-06
### Improvements
- Design changes

## [1.0.0] 2025-02-23
### Platform Re-Invation 
- Restructured the platform from Nodejs backend to python 
-- Using web3py rather than web3js 


### [1.0.1] 2025-02-03 
### Updated Blog Listings Page --- Route-Decorator  (Blog_Listings)
- url -- Blog_Listings 
- parameters --- AccountAddress 


### OFFICIAL BLOCK #######
### [1.0.1] 2025-27-02 -- 14:18 PM 
-- CWDT -- Offchain storage implementation as a TRD database 
-- Has 2 Controllers  
        ### COntrolllers ### 
        -- CWDT_COntrolller -- Modifies , Manages data in/out of the database 
        -- Offchain_Compass -- Initializer scriot for setting up the DB 
                            -- Confirm by running check on folder '~/database/CWDTDB.db ? ' 
                            -- Recreate on lost + fix on broken journals thru MIT intergration 


### [ 1.0.1:1] 2025-02-03 
### Solved Multiple File Upload by Utilitilising request.files.getlist() 
-- Previously Accesssing our File Pointer ( File ) we only used request.file.get 
-- This only returned a copy of one item to the System 
-- Therefore other files were disposed off and only the primary selectio id filtered thru 

        -- To combat this we later introduced request.files.getlist()
        -- Which recevies a file pointer attr and return the file objects in list form 
        -- Follow up url https://www.geeksforgeeks.org/upload-multiple-files-with-flask/ 
        -- Currentlyour nation is asfollows 
        
        \ - Uploadmultiple Files & Receive them thru request.files.getlist(File)
        \-  Save each file to disk using a for loop with the condstructs 
                \- File.save(NotationSignature.filename) 
                \- Notation Signature is the identifier for 1st the object in the for loop
                \- The function takes the File attribute that was supplied at input 



### Authentication System Setup 
## Preventing Double Admission 
## Verifying account details before throwing Dashboard


### [1.0.1.2] 2025-04-03
### Securing Rentrancy Guards  
 - Confirming Account Existense ( Wallet Based) Before applying filtering sec teq
 - If exists(accounts)  
        Update Last Logon and centric sys details 
        Grab customID's and fly  

        