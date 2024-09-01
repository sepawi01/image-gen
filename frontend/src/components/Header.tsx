
type HeaderProps = {
    title: string,
    logo: string
}

export default function Header( { title, logo} : HeaderProps) {
  return (
    <header>
      <div className="pt-5 pl-5 pb-3 flex items-center">
        <img src={logo} alt="logo" className="h-10" />
        <h1 className="text-2xl italic font-roboto ml-8">{ title }</h1>
      </div>
    </header>
  )
}