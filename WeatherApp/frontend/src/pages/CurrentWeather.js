import React, {useState, useEffect} from "react";

const CurrentWeather = () => {

    let [weather, setWeather] = useState([])

    useEffect(() =>{
        getWeather()
    }, [])

    let getWeather = async () => {
        let response = await fetch('http://127.0.0.1:8000/api/v1/currentWeather/')
        let data = await response.json()
        console.log('DATA:', data)
        setWeather(data)
    }

    return(
        <div>
            <div className="weather-list">
                {weather.map((weather, index) =>(
                    <h3 key={index}></h3>
                ))}
            </div>
        </div>
    )
}

export default CurrentWeather