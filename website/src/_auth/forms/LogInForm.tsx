import { useNavigate } from 'react-router-dom'

const LogInForm = () => {
  const navigate = useNavigate()

  return (
    <div>
      <button
        onClick={() => navigate('/signup')}
        className="mt-4 px-4 py-2 bg-blue-500 text-white rounded"
      >
        Go to Sign Up
      </button>
    </div>
  )
}

export default LogInForm