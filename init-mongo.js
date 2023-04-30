db = new Mongo().getDB("mariotoilet");
// Create an empty collection so that it shows up in the UI for Mongo Express
db.createCollection("delete_me");
db.createUser(
    {
        user: "mariotoilet",
        pwd: "luigismansion",
        roles: [
            {
                role: "readWrite",
                db: "mariotoilet"
            }
        ]
    }
);