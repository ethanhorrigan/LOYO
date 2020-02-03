const mongoose = require('mongoose')

const Schema = mongoose.Schema

const userSchema = new Schema ({
    email: String,
    summonerName: String,
    primaryRole: String,
    secondaryRole: String,
    password: String
})

module.exports = mongoose.model('user', userSchema, 'users')