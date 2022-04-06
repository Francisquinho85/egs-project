/*!

=========================================================
* Argon Dashboard React - v1.1.0
=========================================================

* Product Page: https://www.creative-tim.com/product/argon-dashboard-react
* Copyright 2019 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/argon-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React, {useState,useEffect} from "react";
// react plugin used to create google maps
// reactstrap components
import {Card, Container, Row} from "reactstrap";
// core components
import Header from "../../components/Headers/Header.js";
import Maps from "./Maps_Component.js";

const call_time = 1000;


const Maps_Page = () => {

  const [markers, setMarkers] = useState([]);

  useEffect(() => {
    const interval = setInterval(
      () => {
        getAllLocations().then((value) => {
            setMarkers(value)
        }
        );
      }, call_time);

      return () => clearInterval(interval)
    },[]
  )

  const getAllLocations = async () => {
    let response = await fetch(
      `/test/data`);
    let result = await response.json();

    let all_locations = [];
    //console.log(result)
    for (var key in result){
        all_locations.push(
    //     // {
    //     //   lat: result[i]["location"]["lat"],
    //     //   lng: result[i]["location"]["lng"],
    //     //   id: result[i]["id"],
    //     //   status: result[i]["status"]
        // }
      {
          lat: parseFloat(result[key]["lat"]),
          lng: parseFloat(result[key]["lon"]),
          id: key,
          status: 0
        }
      )
    }
    console.log(all_locations.length)
    return all_locations;
  }

  return(
      <>
        <Header />
        {/* Page content */}
        <Container className="mt--7" fluid>
          <Row>
            <div className="col">
              <Card className="shadow border-0">
                <Maps
                  markers={markers}
                  zoom = {13}
                  mapElement={
                    <div style={{ height: `150%`, borderRadius: "inherit" }} />
                  }
                />
              </Card>
            </div>
          </Row>
        </Container>
      </>
    );
  }

export default Maps_Page;
