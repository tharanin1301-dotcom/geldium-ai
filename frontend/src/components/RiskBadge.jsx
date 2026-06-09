const RiskBadge = ({ risk }) => {
  const styles = {
    High: 'bg-red-100 text-red-700 border border-red-300',
    Medium: 'bg-orange-100 text-orange-700 border border-orange-300',
    Low: 'bg-green-100 text-green-700 border border-green-300',
  }
  const dots = {
    High: 'bg-red-500',
    Medium: 'bg-orange-500',
    Low: 'bg-green-500',
  }
  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold ${styles[risk]}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${dots[risk]}`} />
      {risk} Risk
    </span>
  )
}
export default RiskBadge
