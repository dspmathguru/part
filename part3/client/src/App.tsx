import React from 'react'
import './App.css'
import { useQuery, gql } from '@apollo/client'

const ALL_USERS = gql`
  query {
    allUsers {
      id
      username
      role
      user_type
      email
    }
  }
`

interface Users extends Array< {
  id: number
  username: string
  role: string
  user_type: string
  email: string
} > {}

function DisplayUsers() {
  const { loading, error, data } = useQuery(ALL_USERS);
  const allUsers: Users = data?.allUsers

  if (loading) return <p>Loading...</p>
  if (error) return <p>Error : {error.message}</p>

  return <>{allUsers.map(({ id, username, role, user_type, email }) => (
    <li key={id}>
      <h3>{username}</h3>
      role: {role}<br />
      user_type: {user_type}<br />
      email: {email}<br />
      <br />
    </li>
  ))}</>
  }

export default function App() {
  return (
    <div>
      <h2>My first Apollo app 🚀</h2>
      <br />
      <DisplayUsers />
    </div>
  )
}
