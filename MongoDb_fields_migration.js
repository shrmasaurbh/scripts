print('\n');
print('Please wait it may will take some time to complete');
print('....');
print('\n');

// var MongoClient = require('mongodb').MongoClient
//   , Server = require('mongodb').Server;

// var mongoClient = new MongoClient(new Server('localhost', 27017));
// mongoClient.open(function(err, mongoClient) {
//   var db = mongoClient.db("customer");

db.cc_user_profile.find().forEach( function(x) {

    if(!x._id) {
        print('No doc found');
        return;
    }
    print( JSON.stringify(x));
    // if need can apply logic to update myField
    x.created_by = parseInt(x.created_by);
    x.updated_by = parseInt(x.updated_by);
    // x.cc_project_name = "parseInt(x.updated_by)";
	var data = db.cc_user_profile.save(x);
    print(data);
    //db.collectionName.update({_id: doc._id}, {$set: {myField: "newVale"}});
});

print('\n');
print('\n');
print('PROFILE FIELD MIGRATION has been completed :)');
print('\n');
print('\n');


db.cc_user_account.find().forEach( function(x) {

    if(!x._id) {
        print('No doc found');
        return;
    }
    print( JSON.stringify(x));
    // if need can apply logic to update myField
    x.created_by = parseInt(x.created_by);
    x.updated_by = parseInt(x.updated_by);
    // x.cc_project_name = "parseInt(x.updated_by)";
    var data = db.cc_user_account.save(x);
    print(data);
    //db.collectionName.update({_id: doc._id}, {$set: {myField: "newVale"}});
});



print('\n');
print('\n');
print('ACCOUNT FIELD MIGRATION has been completed :)');
print('\n');
print('\n');
