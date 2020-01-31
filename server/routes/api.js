const express = require('express')
const router = express.Router()

const mongoose = require('mongoose')
const db =

router.get('/', (req, res) => {
    res.send('From API Route')
})

module.exports = router