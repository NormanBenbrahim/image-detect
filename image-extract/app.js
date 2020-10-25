'use strict'
require('dotenv')
const fs = require('fs')
const fetch = require('node-fetch')
const util = require('util')
const streamPipeline = util.promisify(require('stream').pipeline)
const puppeteer = require('puppeteer')
const scrollPageToBottom = require('puppeteer-autoscroll-down')

// if the data folder doesn't exist, create it 
if (!fs.existsSync('../data')){
    fs.mkdirSync('../data');
}

// if images folder doesn't exist, create it 
if (!fs.existsSync('../data/images')){
    fs.mkdirSync('../data/images');
}

// download files if they're base64 strings or urls
async function download(url_src, dest) { 
    // check if the url starts with http or if it's a base64 string
    if (url_src.startsWith('http')) {
        const response = await fetch(url_src)
        if (!response.ok) {
            throw new Error(`Unexpected response: ${response.statusText}`)
        }
        await streamPipeline(response.body, fs.createWriteStream(dest))
         
    }
    else {
        const string_stripped = url_src.split(';base64,').pop()
        fs.writeFile(dest, string_stripped, {encoding: 'base64'}, function(err) {
            console.log('an error occured: ' + err)
        })
    }

    return true
}

// for a list of valid queries for searching google this article rocks:
// https://stenevang.wordpress.com/2013/02/22/google-advanced-power-search-url-request-parameters/

// get a list of URLs for download and save it as a json file
async function image_extract(query) {
    // parse the query to work with urls
    const url_query = await query.split(' ').join('+')
    const output_folder = await query.split(' ').join('_')
    const path = `../data/images/${output_folder}`

    // check if output folder already exists, if so exit 
    if (!fs.existsSync(path)){
        fs.mkdirSync(path);
    }
    else {
        console.log(`ERROR:  ${path} already exists, exiting program`)
        process.exit(0)
    }

    // launch the browser
    const browser = await puppeteer.launch({
        headless: false,
        defaultViewport: null/*,
        args: ['--no-sandbox', '--disable-setuid-sandbox'],*/
    });
    const page = await browser.newPage();
    page.setViewport({width: 1280, height: 926})

    const url = 'https://www.google.com/?tbm=isch&tbs=isz:m&q=' + url_query
    await page.goto(url, {waitUntil :"networkidle2"})
    // scripts are usually at the bottom, so this is a good way to select pages that have dynamic selectors
    await page.waitForSelector('script')
    await page.type('input[name="q"]', String.fromCharCode(13)) // type enter
    await page.waitForSelector('input[name="q"]')

    // scroll to bottom of page
    // this returns around 398 results per query. you can extend this to return more
    // but for me that's a good enough amount for training
    const scroll_finish = await scrollPageToBottom(page, 250, 1000) // should return true
    await page.waitForTimeout()

    // get a list of urls
    const images = await page.evaluate(() => Array.from(document.images, e => e.src))
    var result // scope
    for (let i = 0; i < images.length; i++) {
        result = await download(images[i], `${path}/img-${i}.png`)

        if (result === true) {
            console.log('Success:', `${path}/img-${i}.png`, 'has been downloaded successfully.')
        } 
        else {
            console.log('Error:', `${path}/img-${i}.png`, 'was not downloaded.')
            console.error(result)
        }                       
    }

    await browser.close()

}

// parse command line arguments
const args = process.argv.slice(2).join(' ')
image_extract(args)