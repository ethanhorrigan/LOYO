const express = require('express')
const router = express.Router()
const User = require('../models/user')
const mongoose = require('mongoose')
const db = "mongodb://ethan:ethan123@ds215093.mlab.com:15093/fyp-users"


mongoose.connect(db, err => {
    if(err) {
        console.log('Error: ' + err)
    }
    else {
        console.log('Connected to the DB')
    }
})

router.get('/', (req, res) => {
    res.send('From API Route')
})

// Register Post Request

router.post('/register', (req, res) => {
    let userData = req.body
    let user = new User(userData)
    user.save((error, registeredUser) => {
        if (error) {
            console.log(error)
        }
        else {
            res.status(200).send(registeredUser)
        }
    })
})
module.exports = router