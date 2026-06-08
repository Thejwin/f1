import React from 'react'
import Navbar from '../components/navbar/navbar'
import Hero from '../components/hero/hero'

const Home = ({ driver, constructor }) => {
  return (
    <div>
      <Navbar />
      <Hero driver={driver} constructor={constructor} />
    </div>
  )
}

export default Home