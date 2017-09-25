
const gplay = require('google-play-scraper');
const _ = require('lodash');
const Promise = require('bluebird');

const logger = require('../../util/logger');
const db = new (require('../../db/db'))('retriever');

const region = 'uk';

/**
 * Inserts app data into the db using db.js
 * @param {*The app data json that is to be inserted into the databae.} appData
 */
function insertAppData(appData) {
    // Checking version data - correct version to update date
    if (!appData.version || appData.version === 'Varies with device') {
        logger.debug('Version not found defaulting too', appData.updated);

        const formatDate = new Date(appData.updated).toISOString().substring(0, 10);
        appData.version = formatDate;
    }

    // push the app data to the DB
    return db.insertPlayApp(appData, region);
}

// TODO Add Permission list to app Data JSON
async function fetchAppData(searchTerm, numberOfApps, perSecond) {
    const appDatas = await gplay.search({
        term: searchTerm,
        num: numberOfApps,
        throttle: perSecond,
        region: region,
        fullDetail: true,
    });

    // TODO: Move this to DB.
    return Promise.all(_.map(appDatas, async(appData) => {
        logger.debug(`inserting ${appData.title} to the DB`);

        const appExists = await db.doesAppExist(appData).catch(logger.err);
        if (!appExists) {
            return insertAppData(appData).catch((err) => logger.err(err));
        } else {
            logger.debug('App already existing', appData.appId);
            return Promise.reject('App Already Exists');
        }
    }));
}

(async() => {
    const dbRows = await db.getStaleSearchTerms();
    Promise.each(dbRows, async(dbRow) => {
        logger.info(`searching for: ${dbRow.search_term}`);
        return fetchAppData(dbRow.search_term, 60, 1)
            .then(await db.updateLastSearchedDate(dbRow.search_term)
                .catch(logger.err))
            .catch(logger.err);
    });
})();
