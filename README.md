# Booking

Full booking process of a restaurant

## Getting Started

To run our application you need to have both MySQL and Docker installed. If you do not have them installed you can do it from these pages
  - Docker installation: https://www.docker.com/
  - MySQL installation: https://www.mysql.com/downloads/

You also have to clone our repository to your computer:
  - git clone https://github.com/DAT210/Booking.git
  - How to instructions if needed: https://git-scm.com/docs/git-clone

The application exist in two versions :
The standalone version,the front and the back are not separated and work in an autonomous way. This version can be pulled from the “master” branch of our directory
The back-end version, it needs the front from the web repository https://github.com/DAT210/web and both need to run simultaneously.This version can be pulled from the “production” branch https://github.com/DAT210/Booking/tree/production.Furthermore if you only want our front part, you can pull the “group1-booking branch” https://github.com/DAT210/web/tree/group1-booking

## Run the application with Docker

# Standalone version
Use cd into the directory where you cloned the project. From here you have to run these commands: 
  - docker-compose -f "docker-compose.yml" up -d --build
  - docker-compose up

The app will say that it is running on “0.0.0.0:5000”, it can not work depending of your operating system :
You can try “127.0.0.1:5000” if you are on windows

The second option is to type “VIRTUAL_MACHINE_IP:5000”. You can find your own virtual machine ip by simply typing in “docker-machine ip” in a command line terminal. 

# Back-end version :
This version don’t rely on another docker Image which run the database but on the host.

You need to have MySQL installed and edit the “src/static/configDocker.ini” to manage the connection.

You need to run the SQL script “src/static/sql/dat210_booking.sql” to initiate the database.


## Contributors

* **Alvaro Cachero** - Front-end & Back-end developer (https://github.com/alvcascac)
* **David Galante** - Project configuration / Front-end & Back-end developer (https://github.com/folowbaka)
* **Pol Grisart** - Front end & Back end developer (https://github.com/pol-grisart)
* **Cihan Kart** - Front end developer (https://github.com/cihankart)
* **Eskil Hellebø** - Database manager & back end developer (https://github.com/eskimil)
* **Mats Moldesæter** - Project manager / Front-end & Back-end developer (https://github.com/230819)
* **Tobias Sætre** - Front-end & Back-end developer (https://github.com/Tobiasns)

