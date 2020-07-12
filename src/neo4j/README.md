# Neo4j Yelp Dataset Solution

Contains Python scripts to import and model the Yelp challenge dataset into Neo4j respectively.

## Getting Started

### Step 0: Pre-processing the Yelp Dataset

Pre-process the Yelp dataset using the project included in `../datasets/yelp-normalization`. The project has a README that describes how to use it.

### Step 1: Getting Neo4j Community Edition

Download the [Neo4j Community Server](https://neo4j.com/download-center/?ref=web-product-database/#community) (not desktop!)
ZIP or tarball or start the Neo4j Docker container with the `docker-compose.yml` file.

If using the ZIP or tarball, extract the archive to a directory e.g. `$HOME`:
```bash
$ tar -xvzf neo4j-community-x.x.x-unix.tar.gz -C ~/.
```
Note that `x.x.x` would refer to the version you are using.

### Step 2: Server Plugins and Configuration
The `neo4j-community.x.x.x` directory in this project contains details
on the files that need to be changed on the server. Note, the changes must be made on your server files and not on this 
project! This project's directory is simply a demonstration. 

The following files must be changed on the server:

* `plugins/apoc-x.x.x.x-all.jar`: Download the latest [APOC plugin](https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases) and place it under the plugins directory on your server.
* `conf/neo4j.conf`: This has been configured to whitelist the APOC functions we use in the import process. User authentication is also disabled.
* `import/{business, review, user}.json`: All Yelp files one wishes to import must be placed here. This script only considers the three JSON files listed here.
NOTE: running the project in `../datasets/yelp-normalization` creates the necessary files inside `../datasets/norm` or `../datasets/sub`. Please rename the files you import so they comply.

### Step 3: Installing Java

Neo4j requires Java to run. The version of Java necessary for Neo4j to run is dependent on the Neo4j version e.g. Neo4j 4 requires Java 11. 

I recommend using [AdoptOpenJDK](https://adoptopenjdk.net/installation.html?variant=openjdk11&jvmVariant=hotspot) and setting $JAVA_HOME to the location of the directory e.g. `export JAVA_HOME=/home/david/Downloads/jdk-11.0.5+10`.

### Step 4: Starting Neo4j

If not using the Docker image, start Neo4j using the `neo4j` binary in the `neo4j-community-x.x.x/bin` file. Example:
```bash
$ ~/neo4j-community-x.x.x/bin/neo4j start
```
Optionally, one can set their `~/.profile`, `~/.bashrc`, or `~/.zshrc` etc. to add Neo4j binaries to their path by adding the following line: 
```bash
export PATH=/home/david/neo4j-community-x.x.x/bin:$PATH
```
Then one can simply use:
```bash
$ neo4j start
```

Neo4j browser should now be running on `http://localhost:8001`. Default username and password is `neo4j` and `neo4j` respectively. The bolt port is on `http://localhost:8000`. These port numbers are to comply with Stellenbosch University's port policies.

### Step 5: Python Dependencies

Before running the `neo4j_yelp.py` script, make sure that you have installed all of the dependencies and edited `config.py` to contain your credentials. To download all the dependencies you can simply type:
```bash
$ pip3 install -r requirements.txt --user
```

### Step 6: Import the Dataset

Now that everything is configured and ready, the import script can be run with:
```bash
$ python3 neo4j_yelp.py
```
If all goes well, you will see the following output from the terminal:
```bash
[INFO] Clearing graph of any existing data
[INFO] Asserting schema
[INFO] Loading businesses
[INFO] Loading users
[INFO] Loading reviews
```


##

Please don't hesitate to ask Anya or Phillip if there are any questions :)