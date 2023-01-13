/* These are Mongo Shell commands, as documented at https://docs.mongodb.com/manual/mongo/ */

db.createUser(
    {
        user: "user",
        pwd: "password",
        roles:[
            {
                role: "readWrite",
                db:   "db",
            }
        ]
    }
);

db.createCollection("auth");

db.getCollection("auth").insert({
    "user" : "guest",
    "am" : {
        "read_groups" : [
            "public"
        ],
        "write_groups" : [],
        "admin_access" : false
    },
    "password" : "$argon2i$v=19$m=102400,t=2,p=8$S4lRqpWSck7JGWMMgTDGGA$MRa3VgoE5o1qZET5/yBRBA"
});