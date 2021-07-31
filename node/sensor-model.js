const config = require("./config.json");
const { Sequelize, Model, DataTypes } = require('sequelize');
const sequelize = new Sequelize(`mysql://${config.mysql.user}:${config.mysql.password}@${config.mysql.host}:3306/${config.mysql.database}`);

class SensorModel extends Model { }
SensorModel.init({
    distanceCm: DataTypes.FLOAT,
    epochMs: DataTypes.BIGINT
}, { sequelize, modelName: 'sensor', timestamps: false });

sequelize.sync();

module.exports = SensorModel;