import { Navigate, Outlet } from 'react-router-dom'

const AuthLayout = () => {
 const isAuthenticated = false

  return (
    <>
      {isAuthenticated ? (
        <Navigate to="/" />
      ) : (
        <>
          <section className="flex flex-1 justify-center items-center flex-col">
            <Outlet />
          </section>
        </>
      )}
    </>
  )
}

export default AuthLayout
