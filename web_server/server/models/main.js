const mongoose = require('mongoose');

module.exports.connect = (uri) => {
    mongoose.connect(uri);

    mongoose.connection.on('error', (err) => {
        // when user and password error
        console.error('Mongoose connection error: ${err}');
        process.exit(1);
    });

    //load modules
    require('./user');
}
 