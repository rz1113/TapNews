const mongoose = require('mongoose'); 
const bcrypt = require('bcrypt'); //used for salt

const UserSchema = new mongoose.Schema({
    email: {
        type: String,
        index: { unique: true } // avoid some user name
    },

    password: String
});

UserSchema.methods.comparePassword = 
    function comparePassword(password, callback) {
        bcrypt.compare(password, this.password, callback);
    };

UserSchema.pre('save', function saveHook(next) {
    const user = this;
    return bcrypt.genSalt((saltError, salt) => {
        if (saltError) { return next(saltError); }
        return bcrypt.hash(user.password, salt, (hashError, hash) => {
            if (hashError) { return next(hashError); }
            // replace the plain password with the hashed password adding salt
            user.password = hash;
            return next();
        });
    });
});

module.exports = mongoose.model('User', UserSchema);